from django.db import transaction
from django.db.models.functions import Upper
from django.db.models.signals import pre_save
from django.dispatch import receiver

from sunbed.models import Sunbed


@receiver(pre_save, sender=Sunbed)
def auto_fill_sunbed_identity(sender, instance, **kwargs):
    """
    If instance.identity is blank, auto‐generate a 6‐char code: [prefix][zone_part][seq].
    - prefix = up to 2 uppercase initials of `area` (one letter per word, truncated if ≥3 words).
    - zone_part = str(zone.id) (e.g. "3", "12", etc.).
    - seq = zero-padded integer so that total length = 6 (and seq has at least width=1).
    We ensure no two sunbeds in the SAME (zone, uppercase area) end up with the same identity.
    """
    # 1) If identity already set manually, do nothing.
    if instance.identity:
        return

    # 2) Build raw initials from area: take first letter of each word, uppercase.
    #    Then, if that yields ≥ 3 letters, truncate to exactly 2 (so seq can have ≥1 digit).
    words = [w for w in instance.area.split() if w]
    raw_initials = "".join(w[0].upper() for w in words)

    # We want prefix_final to be at most 2 letters, because we need at least 1 digit in the sequence.
    if len(raw_initials) >= 3:
        prefix_final = raw_initials[:2]
    else:
        prefix_final = raw_initials  # length is 1 or 2

    # 3) zone_part is just the decimal string of zone.id.
    zone_part = str(instance.zone.id)

    # 4) Decide how many digits are left for the sequence:
    MAX_ID_LEN = 6
    used_len = len(prefix_final) + len(zone_part)
    # We must leave at least 1 character for the numeric suffix
    numeric_width = MAX_ID_LEN - used_len
    if numeric_width < 1:
        # If numeric_width < 1, it means prefix_final+zone_part is too long.
        # In practice, this happens if zone.id has > 4 digits (e.g. 12345) OR
        # raw_initials was 2 letters and zone_id is 4 digits (“AB” + “1234” => 6 chars),
        # leaving numeric_width=0. In that extreme case, we can truncate prefix_final
        # down to 1 letter so numeric_width becomes >=1. If it STILL fails, raise an error.
        # Adjust logic as your domain requires.
        if len(prefix_final) > 1:
            prefix_final = prefix_final[:1]
            used_len = len(prefix_final) + len(zone_part)
            numeric_width = MAX_ID_LEN - used_len
        if numeric_width < 1:
            raise ValueError(
                f"Cannot auto-generate identity: area initials='{raw_initials}', "
                f"zone_id='{zone_part}' produce no space for a sequence. "
                f"Try shorter area or smaller zone_id."
            )

    # 5) Now, within a single transaction, find the “next” sequence for this (zone, area):
    with transaction.atomic():
        # a) Filter all Sunbeds with same zone & same area (case‐insensitive).
        same_zone_and_area = (
            sender.objects.filter(zone=instance.zone).annotate(
                area_upper=Upper('area')
            ).filter(area_upper=instance.area.upper())
        )

        # b) Among those, pick only the ones whose existing identity begins with prefix_final + zone_part.
        key_prefix = prefix_final + zone_part
        candidates = same_zone_and_area.filter(identity__startswith=key_prefix)

        # c) Extract the numeric suffix of each candidate’s identity, parse to int, track max.
        max_num = 0
        for ident in candidates.values_list('identity', flat=True):
            suffix = ident[len(key_prefix):]  # e.g. if ident="AC1202", key_prefix="AC12", suffix="02"
            try:
                num = int(suffix)
            except (ValueError, TypeError):
                # Skip any identity that doesn’t parse (shouldn’t happen if our own code always writes numeric suffix).
                continue
            if num > max_num:
                max_num = num

        next_num = max_num + 1
        numeric_part = str(next_num).zfill(numeric_width)

        # d) Finally, set instance.identity:
        instance.identity = prefix_final + zone_part + numeric_part

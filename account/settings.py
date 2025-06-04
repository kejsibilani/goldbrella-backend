from helpers.short_func import crud

ADMIN_USER_PERMISSION_SET = {
    # location permissions
    *crud('location'),
    # service permissions
    *crud('facility'),
    *crud('rule'),
    # beach permissions
    *crud('beach'),
    *crud('beachimage'),
    *crud('beachopeninghour'),
    *crud('beachopeningseason'),
    # inventory permissions
    *crud('inventoryitem'),
    # sunbed permissions
    *crud('sunbed'),
    # zone permissions
    *crud('zone'),
    # user permissions
    *crud('user'),
    *crud('shift'),
    # booking permissions
    *crud('booking'),
    *crud('bookinginvoice'),
    *crud('bookingpayment'),
    # complaint permissions
    *crud('complaint'),
    *crud('review'),
    # notification permission
    *crud('notification'),
}

GUEST_USER_PERMISSION_SET = {
    # booking permissions
    'add_booking',
    'view_booking',
    'change_booking',
    'delete_booking',
}

SUPERVISOR_USER_PERMISSION_SET = {
    'add_booking',
    'view_booking',
    'change_booking',
    'delete_booking',
}

STAFF_USER_PERMISSION_SET = {
    'add_booking',
    'view_booking',
    'change_booking',
    'delete_booking',
}

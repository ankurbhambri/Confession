var $btn2 = $('a.collapsed');
$btn2.data('state', 'hover');

var enterShow = function () {
    if ($btn2.data('state') === 'hover') {
        $btn2.popover('show');
    }
};
var exitHide = function () {
    if ($btn2.data('state') === 'hover') {
        $btn2.popover('hide');
    }
};

var clickToggle = function () {
    if ($btn2.data('state') === 'hover') {
        $btn2.popover('show');
        $btn2.data('state', 'show');
    } else {
        $btn2.popover('hide');
        $btn2.data('state', 'hover')
    }
};

$btn2.popover({trigger: 'manual'})
    .on('click', clickToggle);

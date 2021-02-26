$(function () {
    ////activar plugin TouchSpin para la convocatoria
    $("input[name='cantidad']").TouchSpin({
        'verticalbuttons': true,
        'min': 0.00,
        'initval': 0.00,
        'step': 0.1,
        'decimals': 4,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    $("input[name='cupo_autorizado']").TouchSpin({
        'verticalbuttons': true,
        'min': 0.00,
        'initval': 0.00,
        'step': 0.1,
        'decimals': 4,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });
});
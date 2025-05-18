(function() {
    // Usar django.jQuery em vez de $ para evitar conflitos no Django Admin
    var $ = window.django ? window.django.jQuery : window.jQuery;

    if (!$) {
        console.error('jQuery não está disponível!');
        return;
    }

    console.log('Iniciando tutor_mask.js...');
    $(document).ready(function() {
        // Verificar se o Inputmask está carregado
        if (typeof $.fn.inputmask === 'undefined') {
            console.error('jQuery Inputmask não está carregado!');
            return;
        }
        console.log('jQuery Inputmask carregado com sucesso.');

        // Verificar campos disponíveis
        console.log('Campos telefone-mask encontrados:', $('.telefone-mask').length);
        console.log('Campos cpf-mask encontrados:', $('.cpf-mask').length);
        console.log('Campos cep-mask encontrados:', $('.cep-mask').length);

        // Máscara para telefone
        $('.telefone-mask').inputmask({
            mask: '(99) 99999-9999',
            placeholder: '(__) _____-____',
            clearIncomplete: true,
            oncomplete: function() {
                console.log('Telefone preenchido:', $(this).val());
            },
            onincomplete: function() {
                console.log('Telefone incompleto:', $(this).val());
            }
        });

        // Máscara para CPF
        $('.cpf-mask').inputmask({
            mask: '999.999.999-99',
            placeholder: '___-___-___-__',
            clearIncomplete: true,
            oncomplete: function() {
                console.log('CPF preenchido:', $(this).val());
            },
            onincomplete: function() {
                console.log('CPF incompleto:', $(this).val());
            }
        });

        // Máscara para CEP
        $('.cep-mask').inputmask({
            mask: '99999-999',
            placeholder: '_____-___',
            clearIncomplete: true,
            oncomplete: function() {
                console.log('CEP preenchido:', $(this).val());
            },
            onincomplete: function() {
                console.log('CEP incompleto:', $(this).val());
            }
        });

        // Validação ao submeter o formulário
        $('form').submit(function(event) {
            $('.cpf-mask').each(function() {
                const value = $(this).val();
                if (!$(this).inputmask('isComplete')) {
                    console.error('CPF incompleto ou inválido ao submeter:', value);
                    event.preventDefault();
                    alert('Por favor, preencha o CPF corretamente antes de enviar.');
                } else {
                    console.log('CPF válido ao submeter:', value);
                }
            });
        });
    });
})();
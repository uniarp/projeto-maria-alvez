(function($) {
    console.log('Iniciando tutor_mask.js...');
    $(document).ready(function() {
        // Log para verificar se o jQuery e Inputmask estão disponíveis
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
            placeholder: '(11) 91234-5678',
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
            placeholder: '123.456.789-09',
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
            placeholder: '12345-678',
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
})(jQuery);
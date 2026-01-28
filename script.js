console.log('script carregado');
document.addEventListener('DOMContentLoaded', function () {

    // TROCA DE CARDS LOGIN-SENHA
    const forgotLink = document.querySelector('.forgot-password a');
    const loginBox = document.querySelector('.login-box');
    const backCard = document.querySelector('.back-card');

    if (forgotLink && loginBox && backCard) {
        forgotLink.addEventListener('click', function (troca) {
            troca.preventDefault();
            loginBox.style.display = 'none';
            backCard.style.display = 'flex';
        });
    }

    //MÁSCARA DE TELEFONE
    const telInput = document.getElementById('tel');
    if (telInput) {
        telInput.addEventListener('input', function (maskTel) {
            let mt = maskTel.target.value.replace(/\D/g, ''); //remove tudo que não for número
            // maskTel.target = input do telefone
            // \D = qualquer caractere que não seja dígito
            // g = global (remove todos)

            if (mt.length > 11) mt = mt.slice(0, 11);
            //corta valor copiado até o 11º digito
            //slice(0, 11) = índice 0 a 11

            mt = mt.replace(/^(\d{2})(\d)/, '($1) $2');
            //replace = troca /^(\d{2})(\d)/ por ($1) $2
            // ^ = inicio da sytring
            // (\d{2}) = captura os 2 primeiros números (DDD)
            // (\d) = captura o próximo número
            // $1 = DDD / $2 = primeiro número após DDD
            mt = mt.replace(/(\d{5})(\d)/, '$1-$2');
            maskTel.target.value = mt; //atualiza o valor do campo em tempo real
        });
    }

    //MÁSCARA DE CPF
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function (maskCpf) {
            let mc = maskCpf.target.value.replace(/\D/g, '');
            if (mc.length > 11) mc = mc.slice(0, 11);

            mc = mc.replace(/^(\d{3})(\d)/, '$1.$2');
            mc = mc.replace(/(\d{3})(\d)/, '$1.$2');
            mc = mc.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            maskCpf.target.value = mc;
        });
    }

    //MÁSCARA DATA DE NASCIMENTO
    const nascInput = document.getElementById('date');
    if (nascInput) {
        nascInput.addEventListener('input', function (maskNasc) {
            let mn = maskNasc.target.value.replace(/\D/g, '');
            if (mn.length > 8) mn = mn.slice(0, 8);

            mn = mn.replace(/^(\d{2})(\d)/, '$1/$2');
            mn = mn.replace(/(\d{2})(\d)/, '$1/$2');
            mn = mn.replace(/(\d{4})(\d)/, '$1/$2');
            maskNasc.target.value = mn;
        });
    }

    //LIMITES DE IDADE 
    const erroIdade = document.getElementById('erroIdade'); 
    function calcularIdade() {
        if(!nascInput || !erroIdade) return null;
         
        const valor = nascInput.value; 
            
        if(!/^\d{2}\/\d{2}\/\d{4}$/.test(valor)) return null; 
        const [dia, mes, ano] = valor.split('/').map(Number); 
        //split = divide / map(Number) = torna a string do input em número
        const nascimento = new Date(ano, mes - 1, dia); 
            
        const hoje = new Date(); 
        let idade = hoje.getFullYear() - nascimento.getFullYear(); 
        const m = hoje.getMonth() - nascimento.getMonth(); 
            
        if (m < 0 || (m === 0 && hoje.getDate() < nascimento.getDate())) { 
            idade--; 
        } 

        return idade;
    }

    function validarIdade() {
        let valorIdade = calcularIdade();
        console.log(valorIdade);

        if (valorIdade === null) return false;

        if (valorIdade < 18) { 
            erroIdade.style.display = 'block'; 
            nascInput.classList.add('input-erro'); 
            return false;
                    
        } 
        erroIdade.style.display = 'none'; 
        nascInput.classList.remove('input-erro'); 
        return true;
    }

    if (nascInput && erroIdade) {
        nascInput.addEventListener('blur', validarIdade); //blur = perde foco

        nascInput.addEventListener('input', () => {
            erroIdade.style.display = 'none';
            nascInput.classList.remove('input-erro');
        });
    }

    //VALIDAÇÃO DE SENHA
    const passwordBox = document.querySelectorAll('.password-box');

    passwordBox.forEach(passBox => {
        const senhaInput = passBox.querySelector('.password');
        const erroSenha = passBox.querySelector('.erroSenha');

        if (!senhaInput || !erroSenha) return;

        senhaInput.addEventListener('blur', () => {
            validarSenha(senhaInput, erroSenha);
        });

        senhaInput.addEventListener('input', () => {
            erroSenha.style.display = 'none';
            senhaInput.classList.remove('input-erro');
        })
    });

    function validarSenha(senhaInput, erroSenha) {
        if (!senhaInput || !erroSenha) return true;

        if (senhaInput.value.length >= 5 || senhaInput.value === '') {
            erroSenha.style.display = 'none';
            senhaInput.classList.remove('input-erro');
            return true;
        } 
        erroSenha.style.display = 'block';
        senhaInput.classList.add('input-erro');
        return false;
    }

    //VALIDAÇÃO DO CÓDIGO
    const codigoInput = document.getElementById('codigo');

    function validarCodigo() {
        if (!codigoInput) return true;
        const codigo = codigoInput.value.trim();

        if (!/^\d+$/.test(codigo) || codigo === '') { //só permite números inteiros (REGEX)
            codigoInput.classList.add('input-erro');
            return false;
        }
        codigoInput.classList.remove('input-erro');
        return true;
    }

    if (codigoInput) {
        codigoInput.addEventListener('blur', validarCodigo);

        codigoInput.addEventListener('input', () => {
            codigoInput.classList.remove('input-erro');
        });
    }

    //TROCA DE CARDS CODIGO-SENHA
    const codigoButton = document.querySelector('.codigo-button');
    const codigoCard = document.querySelector('.codigo-card');
    const senhaCard = document.querySelector('.senha-card');

    if (codigoButton && codigoCard && senhaCard) {
        codigoButton.addEventListener('click', function (troca2) {
            if (!validarCodigo()) {
                troca2.preventDefault();
                return;
            }
            codigoCard.style.display = 'none';
            senhaCard.style.display = 'flex';
        });
    }

    //VALIDAÇÃO NA TROCA DE SENHA
    const senhaInput1 = document.querySelector('.password1');
    const senhaInput2 = document.querySelector('.password2');
    const erroSenha2 = document.querySelector('.erroSenha2');

    function confirmarSenha() {
        if (!senhaInput1 || !senhaInput2 || !erroSenha2) return true;

        if (senhaInput2.value === '' || senhaInput1.value === senhaInput2.value) {
            erroSenha2.style.display = 'none';
            senhaInput2.classList.remove('input-erro');
            return true;
        }
        erroSenha2.style.display = 'block';
        senhaInput2.classList.add('input-erro');
        return false;
    }

    if (senhaInput1 && senhaInput2 && erroSenha2) {
        senhaInput2.addEventListener('blur', confirmarSenha);

        senhaInput2.addEventListener('input', () => { // sem parâmetro ()
            erroSenha2.style.display = 'none';
            senhaInput2.classList.remove('input-erro');
        });
    }

    //ENVIO DO FORM
    document.querySelectorAll('.signup-form').forEach(form => { //o mesmo que function (form)
        form.addEventListener('submit', function (validarForm) {
            let envio = true;

            if (!form.checkValidity()) {
                envio = false;
            }

            if (form.querySelector('#date') && !validarIdade()) {
                envio = false;
            }

            if (form.querySelector('.password2') && !confirmarSenha()) {
                envio = false;
            }

            form.querySelectorAll('.password-box').forEach(box => {
                const senhaInput = box.querySelector('.password');
                const erroSenha = box.querySelector('.erroSenha');

                if (!validarSenha(senhaInput, erroSenha)) {
                    envio = false;
                }
            });

            if (!envio) {
                validarForm.preventDefault(); 
                form.reportValidity();
            }
        });
    });
});
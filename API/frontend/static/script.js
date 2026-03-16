async function login() {
    const email = document.getElementById('email').value
    const senha = document.getElementById('senha').value

    const resposta = await fetch("/login", {
        method:"POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            email: email,
            senha: senha
        })
    })

    const data = await resposta.json()

    showAlert(data.mensagem, data.status || "error")
}

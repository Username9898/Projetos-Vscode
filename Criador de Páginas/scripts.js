/* 
Lógica de Programação

Algoritmo - Receita de BOLO

[x] Saber quando o botão foi clicado
[x] Pegar o texto do TextArea
[x] Enviar para a IA(servidor)
[x] Pegar a resposta da IA
[x] Colocar na tela
    [x] Código
    [x] Resultado do Código     
[ ] Refinar nosso resultado        

    querySelector - pega um elemento que eu escolher
    HTML - document
    JavaScript - script
*/
let endereco = "https://api.groq.com/openai/v1/chat/completions"

let prompt = `Você é um designer web premiado e Programador. 
Crie uma landing page COMPLETA e VISUALMENTE IMPRESSIONANTE para o negócio descrito.

                    Regras de resposta:
                    - Responda SOMENTE com HTML e CSS puros
                    - Não use crases, markdown ou explicações
                    - Não use tags <img>

                    Identidade visual (capriche e surpreenda):
                    - Invente uma paleta de cores única que combine com a essência do negócio
                    - Escolha uma Google Font marcante via @import
                    - Use emojis grandes no lugar de imagens
                    - Use CSS moderno: gradientes, sombras, animações sutis, layout generoso, tipografia forte

                    Estrutura da página:
                    - Header com nome do negócio e menu
                    - Hero impactante com título, subtítulo e botão CTA
                    - Seção de diferenciais com emojis
                    - Depoimento de cliente
                    - Footer com contato

Todo o conteúdo em português, criativo e específico para o negócio.`


// Clicou no Botão GERAR - Chama essa função
async function gerarCodigo() {


    let textarea = document.querySelector(".texto-pagina").value

    let resposta = await fetch(endereco, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer seu_groq_api_key_aqui"
        },
        body: JSON.stringify({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                // user = usuário - a pessoa que está mexendo no site pede
                // system = quem a IA deve ser
                {
                    "role": "user",
                    "content": textarea
                },
                {
                    "role": "system",
                    "content": prompt
                }
            ],
        })
    })


    let dados = await resposta.json()
    let resultado = dados.choices[0].message.content

    let espacoCodigo = document.querySelector(".bloco-codigo")
    let espacoSite = document.querySelector(".bloco-site")

    espacoCodigo.textContent = resultado
    espacoSite.srcdoc = resultado
}

/* 
IA para gerar o que queremos 

1) Qual o modelo de IA vamos usar
2) system - Quem a IA deve ser - Programador / Designer
3) user - mensagem do usuário

*/


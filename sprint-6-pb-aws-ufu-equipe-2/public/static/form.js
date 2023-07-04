document.addEventListener("DOMContentLoaded", function () {
  const input4 = document.getElementById('input4');
  const btn4 = document.getElementById('btn4');

  const input5 = document.getElementById('input5');
  const btn5 = document.getElementById('btn5');

  const input6 = document.getElementById('input6');
  const btn6 = document.getElementById('btn6');

  function handleClick(url, input) {
    return async function (event) {
      event.preventDefault();

      try {
        const requestBody = {
          phrase: input.value
        };

        const response = await fetch(url, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        const data = await response.json();
        const phraseElement = document.getElementById("phrase");
        const urlElement = document.getElementById("url");
        const dataElement = document.getElementById("data");
        const idElement = document.getElementById("id");

        phraseElement.textContent = `"received_phrase": "${data.received_phrase}"`;
        urlElement.textContent = `"url_to_audio": "${data.url_to_audio}"`;
        dataElement.textContent = `"created_audio": "${data.created_audio}"`;
        idElement.textContent = `"unique_id": "${data.unique_id}"`;

        const result = document.querySelector(".result");
        result.style.display = "block";
      } catch (error) {
        console.log(error);
      }
    };
  }

  btn4.addEventListener("click", handleClick("/v1/tts", input4));
  btn5.addEventListener("click", handleClick("/v2/tts", input5));
  btn6.addEventListener("click", handleClick("/v3/tts", input6));
});
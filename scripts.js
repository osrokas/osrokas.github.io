function renderCards() {
  var container = document.getElementById("cards-container");
  cards.forEach(function (card) {
    var div = document.createElement("div");
    div.className = "card";
    div.style.width = "18rem";
    div.style.margin = "10px";
    div.innerHTML =
      '<div class="card-body">' +
      "<h5 class=\"card-title\">" + card.title + "</h5>" +
      "<p class=\"card-text\">" + card.text + "</p>" +
      "<a href=\"" + card.link + "\" style=\"color: aliceblue; font-weight: bold; font-size: large\">" + card.linkText + "</a>" +
      "</div>";
    container.appendChild(div);
  });
}

renderCards();

consoleText(
  [
    "Machine learning practitioner",
    "Software engineering",
    "Data engineering",
  ],
  "text",
  ["tomato", "rebeccapurple", "lightblue"]
);

function consoleText(words, id, colors) {
  if (colors === undefined) colors = ["#fff"];
  var visible = true;
  var con = document.getElementById("console");
  var letterCount = 1;
  var x = 1;
  var waiting = false;
  var target = document.getElementById(id);
  target.setAttribute("style", "color:" + "white");
  window.setInterval(function () {
    if (letterCount === 0 && waiting === false) {
      waiting = true;
      target.innerHTML = words[0].substring(0, letterCount);
      window.setTimeout(function () {
        var usedColor = colors.shift();
        colors.push(usedColor);
        var usedWord = words.shift();
        words.push(usedWord);
        x = 1;
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (letterCount === words[0].length + 1 && waiting === false) {
      waiting = true;
      window.setTimeout(function () {
        x = -1;
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (waiting === false) {
      target.innerHTML = words[0].substring(0, letterCount);
      letterCount += x;
    }
  }, 120);
  window.setInterval(function () {
    if (visible === true) {
      con.className = "console-underscore hidden";
      visible = false;
    } else {
      con.className = "console-underscore";

      visible = true;
    }
  }, 400);
}

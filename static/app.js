function returnResponse(res, img_url = "") {
  console.log("enter");

  html =
    '<div class="messages__item messages__item--visitor">' +
    res +
    "</br>" +
    `<img src="${img_url}" alt="${"This is image"}">` +
    "</div>";

  return html;
}

class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };
    this.state = false;
    this.message = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    //show or hides the box
    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.message.push(msg1);

    // 'http://127.0.0.1:5000/predict
    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "Sam", message: r.answer };
        this.message.push(msg2);
        this.updateChatText(chatbox);
        textField.value = "";
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
      });
  }

  updateChatText(chatbox) {
    var html = "";
    this.message
      .slice()
      .reverse()
      .forEach(function (item) {
        console.log(item);
        if (item.name === "Sam") {
          for (let sub_mess of item.message)
            if (sub_mess[0] === "BookRestaurant") {
              console.log(sub_mess);
              for (let restaurant of sub_mess[1]) {
                let res_mess =
                  "name: " +
                  restaurant.name +
                  "\nnumber of rating: " +
                  restaurant.number_of_rating;
                html += returnResponse(res_mess, restaurant["img_url"]);
              }
            } else if (sub_mess[0] === "GetWeather") {
              let res_mess =
                "date: " + sub_mess[1].date + "\n" + sub_mess[1].temperature;
              html += returnResponse(res_mess, sub_mess[1]["img_url"]);
            } else if (sub_mess[0] === "Error") {
              html +=
                '<div class="messages__item messages__item--visitor">' +
                sub_mess[1] +
                "</div>";
            }
        } else if (item.name === "User") {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();

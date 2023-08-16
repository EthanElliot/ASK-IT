var formats = [
  "bold",
  "code",
  "italic",
  "link",
  "underline",
  "header",
  "list",
  "direction",
  "formula",
  "script",
];

var quill = new Quill("#body_input", {
  modules: {
    toolbar: [
      ["bold", "italic", "underline"],
      [{ script: "super" }, { script: "sub" }],
      [{ list: "ordered" }, { list: "bullet" }, ,],
      ["link"],
      ["clean"],
    ],
  },
  placeholder: "e.g. Have you tried...",
  theme: "snow",
  formats: formats,
});
var form = $("#form");
var parent = null;

form.on("submit", function () {
  var delta = quill.root.innerHTML;
  $("#body").val(JSON.stringify(delta));
  console.log(parent);
  $("#parent").val(parent);
});

//
//
//

async function request_responses(response_id, parent_id) {
  console.log(parent_id);
  let response = await fetch(`/r/${response_id}`, {
    method: "POST",
    body: JSON.stringify({
      parent_id: parent_id,
    }),
  });
  return response.json();
}

const template = document.querySelector("#question_reply_template");

const responses_body = document.querySelector("#question_replies");

function format_responses(response_id, parent_id) {
  response = request_responses(response_id, parent_id).then((data) => {
    data.forEach((response) => {
      // clone the template
      const clone = template.content.cloneNode(true);
      //format template
      clone.querySelector("#question_reply_template_date").innerHTML = new Date(
        response.date_posted
      )
        .toLocaleString("en-GB", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
          timeZone: "GMT",
        })
        .replace(/,/, "");

      console.log(response);

      clone.querySelector(
        "#question_reply_template_user"
      ).innerHTML = `@${response.username}`;
      clone
        .querySelector("#question_reply_template_user")
        .setAttribute("href", `/u/${response.user_id}`);

      clone.querySelector("#question_reply_template_votes").innerHTML =
        response.votes;
      clone.querySelector("#question_reply_template_voteby").innerHTML =
        response.voted_by_user;
      clone.querySelector("#question_reply_template_body").innerHTML =
        response.body;

      clone
        .querySelector("#question_reply_template_reply")
        .setAttribute("href", "#form");
      clone
        .querySelector("#question_reply_template_reply")
        .addEventListener("click", function () {
          parent = response.id;
          document.getElementById(
            "form_replying_to"
          ).innerHTML = `replying to: ${response.username}`;
        });
      //append template
      responses_body.appendChild(clone);
    });
  });
}

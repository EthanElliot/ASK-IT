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

async function request_responses(question_id, parent_id) {
  let response = await fetch(`/r/${question_id}`, {
    method: "POST",
    body: JSON.stringify({
      parent_id: parent_id,
    }),
  });
  return response.json();
}

const template = document.querySelector("#question_reply_template");

const responses_body = document.querySelector("#question_replies");

function format_responses(responses, target_location) {
  responses.forEach((response) => {
    // clone the template
    const clone = template.content.cloneNode(true);
    //format template
    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_date"
    ).innerHTML = new Date(response.date_posted)
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
      "#question_reply_template_wrapper #question_reply_template_user"
    ).innerHTML = `@${response.username}`;
    clone
      .querySelector("#question_reply_template_user")
      .setAttribute("href", `/u/${response.user_id}`);

    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_votes"
    ).innerHTML = response.votes;
    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_voteby"
    ).innerHTML = response.voted_by_user;
    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_body"
    ).innerHTML = response.body;

    clone
      .querySelector(
        "#question_reply_template_wrapper  #question_reply_template_upvote"
      )
      .addEventListener("click", function () {
        update_vote(response.id, 1);
      });
    clone
      .querySelector(
        " #question_reply_template_wrapper #question_reply_template_downvote"
      )
      .addEventListener("click", function () {
        update_vote(response.id, 0);
      });

    clone
      .querySelector(
        "#question_reply_template_wrapper  #question_reply_template_reply"
      )
      .setAttribute("href", "#form");
    clone
      .querySelector(
        "#question_reply_template_wrapper #question_reply_template_reply"
      )
      .addEventListener("click", function () {
        parent = response.id;
        document.getElementById(
          "form_replying_to"
        ).innerHTML = `replying to: ${response.username}`;
      });
    let children = clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_children"
    );
    clone
      .querySelector(
        "#question_reply_template_wrapper #question_reply_template_resonses"
      )
      .addEventListener("click", function () {
        console.log(children);
        responses = request_responses(question_id, response.id).then((data) => {
          format_responses(data, children);
        });
      });
    //append template
    target_location.appendChild(clone);
  });
}

function update_vote(response_id, vote_state) {
  return fetch(`/v/${response_id}`, {
    method: "POST", // Use 'POST' for sending data
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(vote_state),
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    return response.json();
  });
}

$(window).on("load", function () {
  responses = request_responses(question_id, null).then((data) => {
    format_responses(data, responses_body);
  });
});

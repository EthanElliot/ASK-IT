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
  let response = await fetch(`/get_responses/${question_id}`, {
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
    //format template variables
    let vote_count = clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_votes"
    );
    let votes = clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_voteby"
    );
    var upvote_ico = clone.querySelector(
      " #question_reply_template_wrapper #question_reply_template_upvote"
    );
    var downvote_ico = clone.querySelector(
      " #question_reply_template_wrapper #question_reply_template_downvote"
    );
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

    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_user"
    ).innerHTML = `@${response.username}`;
    clone
      .querySelector("#question_reply_template_user")
      .setAttribute("href", `/u/${response.user_id}`);

    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_votes"
    ).innerHTML = response.sum_votes;
    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_voteby"
    ).innerHTML = response.votes;
    clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_body"
    ).innerHTML = response.body;
    console.log(response.votes);
    clone
      .querySelector(
        "#question_reply_template_wrapper  #question_reply_template_upvote"
      )
      .addEventListener("click", function () {
        if (response.voted_by_user[0] === false) {
          alert("you must be signed in to vote");
        } else {
          update_vote(response.id, 1).then((data) => {
            vote_count.innerHTML =
              parseFloat(vote_count.innerHTML) + data.delta;
            votes.innerHTML = response.votes;
            if (data.state === true) {
              upvote_ico.classList.add("icon_fill");
              downvote_ico.classList.remove("icon_fill");
              votes.innerHTML = parseFloat(votes.innerHTML) + 1;
            }
            if (data.state === null) {
              upvote_ico.classList.remove("icon_fill");
              downvote_ico.classList.remove("icon_fill");
            }
          });
        }
      });

    clone
      .querySelector(
        " #question_reply_template_wrapper #question_reply_template_downvote"
      )
      .addEventListener("click", function () {
        //if the user isnt logged tell them
        if (response.voted_by_user[0] === false) {
          alert("you must be signed in to vote");
        } else {
          update_vote(response.id, 0).then((data) => {
            //update the vote
            vote_count.innerHTML =
              parseFloat(vote_count.innerHTML) + data.delta;
            votes.innerHTML = response.votes;

            //update the vote icon
            if (data.state === false) {
              upvote_ico.classList.remove("icon_fill");
              downvote_ico.classList.add("icon_fill");
              votes.innerHTML = parseFloat(votes.innerHTML) + 1;
            }
            if (data.state === null) {
              upvote_ico.classList.remove("icon_fill");
              downvote_ico.classList.remove("icon_fill");

              votes.innerHTML = parseFloat(votes.innerHTML);
            }
          });
        }
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
        if (response.voted_by_user[0] === false) {
          alert("you must be signed in to add a reply");
        } else {
          parent = response.id;
          document.getElementById(
            "form_replying_to"
          ).innerHTML = `replying to: ${response.username}`;
        }
      });

    let children = clone.querySelector("#question_reply_template_children");
    let get_responses = clone.querySelector(
      "#question_reply_template_wrapper #question_reply_template_resonses"
    );
    if (response.num_child > 0) {
      clone.querySelector(
        "#question_reply_template_wrapper #question_reply_template_resonses"
      ).innerHTML = "show replies";
      clone
        .querySelector(
          "#question_reply_template_wrapper #question_reply_template_resonses"
        )
        .addEventListener("click", function handleClick() {
          get_responses.removeEventListener("click", handleClick);
          responses = request_responses(question_id, response.id).then(
            (data) => {
              format_responses(data, children);
            }
          );
        });
    }
    //manipulate styles of clone
    if (response.voted_by_user[0]) {
      if (response.voted_by_user[1] === true) {
        clone
          .querySelector(
            " #question_reply_template_wrapper #question_reply_template_upvote"
          )
          .classList.add("icon_fill");
      }
      if (response.voted_by_user[1] === false) {
        clone
          .querySelector(
            " #question_reply_template_wrapper #question_reply_template_downvote"
          )
          .classList.add("icon_fill");
      }
    }

    if (response.parent_id !== null) {
      clone
        .querySelector(" #question_reply_template_wrapper")
        .classList.add("ml-4");
    }

    //append template
    target_location.appendChild(clone);
  });
}

function update_vote(response_id, vote_state) {
  return fetch(`/update_vote/${response_id}`, {
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
    responses_body.innerHTML = "";
    format_responses(data, responses_body);
  });
});

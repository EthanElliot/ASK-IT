// Get references to the dom elements
var scroller = document.querySelector("#scroller");
var template = document.querySelector("#account_question");
var sentinel = document.querySelector("#sentinel");
var filter = document.querySelector("#filter");

// Set a counter to count the items loaded
var counter = 0;

// Function to request new items and render to the dom
function loadItems() {
  let f = JSON.parse(filter.value);

  // Use fetch to request data and pass the counter value in the QS
  fetch(
    `/get_questions?count=${counter}&user_id=${user_id}&order_direction=${f[0]}&order_by=${f[1]}`
  ).then((response) => {
    // Convert the response data to JSON
    response.json().then((data) => {
      // If empty JSON, exit the function
      if (!data.length) {
        if (counter === 0) {
          // Replace the spinner with "No more posts"
          sentinel.innerHTML = "No posts";
        } else {
          // Replace the spinner with "No more posts"
          sentinel.innerHTML = "No more posts";
        }
        return;
      }

      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {
        // Clone the HTML template
        let template_clone = template.content.cloneNode(true);

        // Query & update the template content
        template_clone.querySelector(
          "#account_question_title"
        ).innerHTML = ` ${data[i].title}`;
        template_clone
          .querySelector("#account_question_title")
          .setAttribute("href", `/q/${data[0].id}`);
        template_clone.querySelector(
          "#account_question_subject"
        ).innerHTML = `${data[i].subject}`;
        template_clone.querySelector(
          "#account_question_date_posted"
        ).innerHTML = new Date(`${data[i].date_posted}`)
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
        template_clone.querySelector(
          "#account_question_body"
        ).innerHTML = `${data[i].body}`;
        template_clone.querySelector(
          "#account_question_views"
        ).innerHTML = `${data[i].views}`;
        template_clone.querySelector(
          "#account_question_saves"
        ).innerHTML = `${data[i].saves}`;

        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;
      }
    });
  });
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver((entries) => {
  // If intersectionRatio is 0, the sentinel is out of view
  console.log("yes");
  // and we don't need to do anything. Exit the function
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  // Call the loadItems function
  loadItems();
  return;
});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);

filter.addEventListener("change", function () {
  counter = 0;
  scroller.innerHTML = "";
  return;
});

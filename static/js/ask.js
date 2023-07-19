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
  placeholder: "e.g. I was trying to...",
  theme: "snow",
  formats: formats,
});

var form = $("#form");

form.on("submit", function () {
  var delta = quill.root.innerHTML;
  console.log(delta);
  $("#body").val(JSON.stringify(delta));
});

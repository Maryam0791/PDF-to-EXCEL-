async function convert() {
  const file = document.getElementById("pdfFile").files[0];

  if (!file) {
    alert("Please select a PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/convert", {
    method: "POST",
    body: formData
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "Converted.xlsx";
  a.click();
}

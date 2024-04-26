export const GET_FILE = (url) => {
  var new_url = window.location.origin + url;
  const data = fetch(new_url, { responseType: "arraybuffer" })
    .then((res) => {
      return res.blob();
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      window.open(url);
    })
    .catch((error) => console.log(error));
  return data;
};

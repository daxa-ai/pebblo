export const GET_FILE = (url) => {
  const data = fetch(url, { responseType: "arraybuffer" })
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

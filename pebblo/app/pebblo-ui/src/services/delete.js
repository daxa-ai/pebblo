const DELETE_METHOD = { method: "DELETE" };

export const DELETE_APP = async (apiEndpoint) => {
  var url = window.location.origin + apiEndpoint;
  const data = fetch(url, DELETE_METHOD)
    .then((res) => {
      return res;
    })
    .catch((error) => console.log(error));
  return data;
};

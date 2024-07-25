export const showSnackbar = (message, callback, timeout = 2000) => {
  let snackbar = document.getElementById("snackbar");
  snackbar.innerHTML = message;
  snackbar.className = "show";
  setTimeout(function () {
    snackbar.className = snackbar.className.replace("show", "");
    callback();
  }, timeout);
};

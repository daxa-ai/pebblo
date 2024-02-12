const IconButton = (props) => {
  const { className, id, type, children } = props;

  return /*html*/ `
      <button ${id ? `id="${id}"` : ""} class="icon-button">
         ${children}
      </button>
    `;
};

export default IconButton;

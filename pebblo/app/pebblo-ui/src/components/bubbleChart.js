import { waitForElement } from "../util.js";

export const BubbleChart = (props) => {
  waitForElement("#bubbleChart", 5000).then(function () {
    const { showTitlesForValues, chartData: data } = props;
    // Set the dimensions and margins of the graph
    const width =
      document.getElementById("graph-container").offsetWidth || 1000;
    let height = document.getElementById("graph-container").offsetHeight || 250;
    const margin = 1;
    const parentHeight =
      document.getElementById("display_pane").offsetHeight || 800;

    const color = d3
      .scaleOrdinal()
      .domain(["entity", "topic"])
      .range(["#BAC5FA", "#B2DDF6"]);

    const nodeHeight = data.length * 10 + 200;
    height = nodeHeight > parentHeight ? parentHeight - 80 : nodeHeight;
    const names = (d) => d?.label?.split(" ");

    const pack = d3
      .pack()
      .size([width - margin * 2, height])
      .padding(1);

    const root = pack(d3.hierarchy({ children: data }).sum((d) => d.value));

    // Create the SVG container.
    const svg = d3
      .select("#bubbleChart")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-margin, -margin, width, height])
      .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;")
      .attr("text-anchor", "middle");

    // Place each (leaf) node according to the layout’s x and y values.
    const node = svg
      .append("g")
      .selectAll()
      .data(root.leaves())
      .join("g")
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

    var tooltip = d3
      .select("#bubbleChart")
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "black")
      .style("border-radius", "5px")
      .style("padding", "10px")
      .style("color", "white")
      .style("position", "absolute");

    var showTooltip = function (event, d) {
      const xPos = event.clientX;
      const yPos = event.clientY;
      tooltip.transition().duration(200);
      tooltip
        .style("opacity", 1)
        .html(
          /*html*/ `<div class="tooltip">
            <div class="tooltip-heading">${d.data.label}</div>
            <div class="tooltip-body">Snippet Count: ${d.data.value}</div>
        <div>`
        )
        .style("left", xPos + 15 + "px")
        .style("top", yPos + "px");
    };

    var hideTooltip = function (event, d) {
      tooltip.transition().duration(200).style("opacity", 0);
    };

    var moveTooltip = function (event, d) {
      const xPos = event.clientX;
      const yPos = event.clientY;
      tooltip.style("left", xPos + 15 + "px").style("top", yPos + "px");
    };

    node
      .append("circle")
      .attr("fill-opacity", 0.7)
      .attr("fill", (d) => color(d.data.type))
      .attr("r", (d) => d.r)
      .on("mouseover", showTooltip)
      .on("mouseleave", hideTooltip)
      .on("mousemove", moveTooltip);

    const text = node
      .append("text")
      .attr("clip-path", (d) => `circle(${d.r})`)
      .attr("class", (d) => {
        if (showTitlesForValues.includes(d.data.value)) {
          return "show-node";
        } else {
          return "hide-node";
        }
      })
      .on("mouseover", showTooltip)
      .on("mouseleave", hideTooltip);

    text
      .selectAll()
      .data((d) => names(d.data))
      .join("tspan")
      .attr("x", 0)
      .attr("y", (d, i, nodes) => `${i - nodes.length / 2 + 0.35}em`)
      .text((d) => d);

    // Add a tspan for the node’s value.
    text
      .append("tspan")
      .attr("x", 0)
      .attr("y", (d) => `${names(d.data).length / 2 + 0.5}em`)
      .attr("fill-opacity", 0.7)
      .attr("class", "bubble-count")
      .text((d) => {
        return d.data.value;
      });

    return Object.assign(svg.node(), { scales: { color } });
  });

  return /*html*/ `
  <div class="graph-container" id="graph-container">
    <div id="bubbleChart"></div>
  </div>
  `;
};

const width = window.innerWidth;
const height = window.innerHeight;
const colors = {

};


document.getElementById("loading").style.display = "flex";

fetch('/rjson')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        generateChart(data)
        
        document.getElementById("loading").style.display = "none";
    })
    .catch(error => console.error(error));


const generateChart = data => {
    const bubble = data => d3.pack()
        .size([width, height])
        .padding(2)(d3.hierarchy({ children: data }).sum(d => d.id));

    const root = bubble(data);

    const svg = d3.select('#bubble-chart')
        .style('width', width)
        .style('height', height);

    const tooltip = d3.select('.tooltip');

    const node = svg.selectAll()
        .data(root.children)
        .enter().append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    + node.transition()
        .ease(d3.easeExpInOut)
        .duration(1000)
        .attr('transform', d => `translate(${d.x}, ${d.y})`);

    const circle = node.append('circle')
        .attr('r', d => d.r)
        .style('fill', function (d) {
            const imageUrl = d.data["imageURL"];
          
            if (imageUrl) {
                return `url(#pattern-${imageUrl})`;
            } else {
                return colors[d.data.artistName];
            }
        });

    const pattern = node.append("svg:pattern")
        .attr("id", function (d) { return `pattern-${d.data["imageURL"]}`; })
        .attr("patternContentUnits", "objectBoundingBox")
        .attr("width", 1)
        .attr("height", 1);

    pattern.append("svg:image")
        .attr("xlink:href", function (d) { return d.data["imageURL"]; })
        .attr("width", 1)
        .attr("height", 1)
        .attr("preserveAspectRatio", "none");


    circle.transition()
        .ease(d3.easeExpInOut)
        .duration(1000)
        .attr('r', d => d.r);

};






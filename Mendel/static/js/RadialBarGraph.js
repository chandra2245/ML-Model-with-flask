
function d3RadialBarGraphBase() {

    var margin = {top: 30, right: 5, bottom: 0, left: 0},
    width = 380 - margin.left - margin.right,
    height = 380 - margin.top - margin.bottom,
    colorBar = d3.scaleOrdinal(d3.schemeCategory10),
    barPadding = 1,
    misc = {ylabel: 7, xlabelH : 5, title:11};
    
    return {
        margin : margin, 
        width : width, 
        height : height, 
        colorBar : colorBar, 
        barPadding : barPadding,
        misc: misc
    };
}


function d3RadialBarGraph(dataset,divid,svgid,group,titletext) {
	var basics = d3RadialBarGraphBase();
	
	var margin = basics.margin,
		width = basics.width,
	    height = basics.height,
		colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc,
		chartRadius = (height) / 2 - 40;
		;



     var data = [];
     for (x in dataset) {
             if(dataset[x].group==group){
                 data.push(dataset[x]);
           } 
         }



const color = d3.scaleOrdinal(d3.schemeCategory10);

let svg = d3.select(divid).append('svg')
  .attr('width', width)
  .attr('height', height)
  .attr("id","radialChartPlot"+svgid)
  .append('g')
    .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

	
let tooltip = d3.select('body').append('div')
  .attr('class', 'tooltips')
  .attr('id',"tooltip"+svgid);

const PI = Math.PI,
  arcMinRadius = 10,
  arcPadding = 10,
  labelPadding = -5,
  numTicks = 10;




  let scale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.measure) * 1.1])
    .range([0, 2 * PI]);

  let ticks = scale.ticks(numTicks).slice(0, -1);
  let keys = data.map((d, i) => d.category);
  //number of arcs
  const numArcs = keys.length;
  const arcWidth = (chartRadius - arcMinRadius - numArcs * arcPadding) / numArcs;

  let arc = d3.arc()
    .innerRadius((d, i) => getInnerRadius(i))
    .outerRadius((d, i) => getOuterRadius(i))
    .startAngle(0)
    .endAngle((d, i) => scale(d))


	
  let radialAxis = svg.append('g')
    .attr('class', 'r axis')
    .selectAll('g')
      .data(data)
      .enter().append('g');

  radialAxis.append('circle')
    .attr('r', (d, i) => getOuterRadius(i) + arcPadding);



  let axialAxis = svg.append('g')
    .attr('class', 'a axis')
    .selectAll('g')
      .data(ticks)
      .enter().append('g')
        .attr('transform', d => 'rotate(' + (rad2deg(scale(d)) - 90) + ')');

  axialAxis.append('line')
    .attr('x2', chartRadius);

  axialAxis.append('text')
    .attr('x', chartRadius + 10)
    .style('text-anchor', d => (scale(d) >= PI && scale(d) < 2 * PI ? 'end' : null))
    .attr('transform', d => 'rotate(' + (90 - rad2deg(scale(d))) + ',' + (chartRadius + 10) + ',0)')
    .text(d => d);

  //data arcs
  let arcs = svg.append('g')
    .attr('class', 'data')
    .selectAll('path')
      .data(data)
      .enter().append('path')
      .attr('class', 'arc')
      .style('fill', (d, i) => d.color)
      
  arcs.transition()
    .delay((d, i) => i * 200)
    .duration(1000)
    .attrTween('d', arcTween);

  arcs.on('mousemove', showTooltip)
  arcs.on('mouseout', hideTooltip)


  function arcTween(d, i) {
    let interpolate = d3.interpolate(0, d.measure);
    return t => arc(interpolate(t), i);
  }

  function showTooltip(d) {
tooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
      .style('display', 'inline-block')
      .html(d.category+": "+d.measure);
  }

  function hideTooltip() {
    tooltip.style('display', 'none');
  }

  function rad2deg(angle) {
    return angle * 180 / PI;
  }

  function getInnerRadius(index) {
    return arcMinRadius + (numArcs - (index + 1)) * (arcWidth + arcPadding);
  }

  function getOuterRadius(index) {
    return getInnerRadius(index) + arcWidth;
  }
  
	  
  
  
  svg.selectAll("mydots")
  .data(data)
  .enter()
  .append("circle")
    .attr("cx", -(width/2)+10)
    .attr("cy", function(d,i){ return -(height/2)+10 + i*25}) 
    .attr("r", 7)
    .style("fill", function(d){ return d.color})

// Add one dot in the legend for each name.
svg.selectAll("mylabels")
  .data(data)
  .enter()
  .append("text")
    .attr("x", -(width/2)+30)
    .attr("y", function(d,i){ return -(height/2)+10 + i*25}) 
    .text(function(d){ return d.category+": "+d.measure})
    .attr("text-anchor", "left")
    .style("alignment-baseline", "middle")
  

}
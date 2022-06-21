function updateBarChart_v2(group, colorChosen, datasetBarChart) {
	
    d3.select('#tooltipbarChart_v2').remove();

   let tooltip = d3.select('body').append('div')
      .attr('class', 'tooltips')
      .attr('id',"tooltipbarChart_v2");
    
    function showTooltip(d) {
       tooltip.style('left', (d3.event.pageX+10) + 'px')
       .style('top', (d3.event.pageY-10) + 'px')
       .style('display', 'inline-block')
       .html(d.category+": "+d.value);
    }

  function hideTooltip() {
    tooltip.style('display', 'none');
  }

    var currentDatasetBarChart = datasetBarChosen_v2(group, datasetBarChart);
    
    var basics = d3BarChartBase_v2();

    var margin = basics.margin,
        width = basics.width,
       height = basics.height,
        colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc
        ;
    
    var 	xScale = d3.scaleLinear()
        .domain([0, currentDatasetBarChart.length])
        .range([0, width])
        ;
    
        
    var yScale = d3.scaleLinear()
      .domain([0, 5])
      .range([height-36,0])
      ;
      
   var svg = d3.select("#barChart_v2 svg");
    
   // Title
   svg.selectAll("text.title") 
        .attr("x", (width + margin.left + margin.right)/2)
        .attr("y", misc.title)
        .attr("class","title")				
        .attr("text-anchor", "middle")
        .text("Average Parameters of all Accounts of Cluster "+group)
    ;
      
   var plot = d3.select("#barChart_v2Plot1")
       .datum(currentDatasetBarChart)
       ;


   var bar=plot.selectAll("rect")
      .data(currentDatasetBarChart);
      

        bar.transition()
        .duration(750)
        .attr("x", function(d, i) {
            return xScale(i);
        })
       .attr("width", width / currentDatasetBarChart.length - barPadding)   
        .attr("y", function(d) {
            return yScale(d.measure);
        })  
        .attr("height", function(d) {
            return height-36-yScale(d.measure);
        })
        .attr("fill", colorChosen)
        ;

        

       bar.on("mouseover", showTooltip);
       bar.on("mouseout", hideTooltip);
    
    plot.selectAll("text.yAxis")
        .data(currentDatasetBarChart)
        .transition()
        .duration(750)
       .attr("text-anchor", "middle")
       .attr("x", function(d, i) {
               return (i * (width / currentDatasetBarChart.length)) + ((width / currentDatasetBarChart.length - barPadding) / 2);
       })
       .attr("y", function(d) {
               return yScale(d.measure) - misc.ylabel;
       })
       .text(function(d) {
            return formatAsInteger(d.measure);
       })
       .attr("class", "yAxis")					 
    ;
    
}

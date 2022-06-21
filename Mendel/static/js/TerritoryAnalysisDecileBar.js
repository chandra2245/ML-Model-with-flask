
function d3DecileBarChart(dataset,chartID) {
    
    var   hbardiv=d3.select("#"+chartID);

    var margin = {top: 20, right: 20, bottom: 35, left: 40},
        width = parseInt(hbardiv.style("width")) - margin.left - margin.right,
        height = 120 - margin.top - margin.bottom;
    
    // set the ranges
    var x = d3.scaleBand()
              .range([0, width])
              .paddingInner(.1)
              .paddingOuter(.3);


    var y = d3.scaleLinear()
              .range([height, 0]);
              
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#"+chartID).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");
    
    var data = [];
    for (i in dataset) {
             if(dataset[i].group=='Decile'){
                 data.push(dataset[i]);
           } 
         }
   
      // format the data
      data.forEach(function(d) {
        d.value = +d.value;
      });
    
      // Scale the range of the data in the domains
      x.domain(data.map(function(d) { return d.type; }));
      y.domain([0, d3.max(data, function(d) { return d.value; })]);
    
      // append the rectangles for the bar chart
      svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.type); })
          .attr("width", x.bandwidth())
          .attr("y", function(d) { return y(d.value); })
          .attr("height", function(d) { return height - y(d.value); })
          .attr("fill","#3cb371");

     svg.selectAll(".text")  		
	  .data(data)
	  .enter()
	  .append("text")
	  .attr("class","label")
	  .attr("x", (function(d) { return x(d.type)-10 + x.bandwidth() / 2 ; }  ))
	  .attr("y", function(d) { return y(d.value) -10; })
	  .attr("dy", ".75em")
	  .text(function(d) { return d.value; });  


  // add the x Axis
  svg.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
	  .selectAll("text")	
        .style("text-anchor", "middle")
		 .attr("class","xlabelbar")
      .select(".domain")
      .remove();

  // add the y Axis
  //svg.append("g")
  //   .call(d3.axisLeft(y));

	// Y axis label
	svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 5 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .attr("class","sidelabel")
      .style("text-anchor", "middle")
      .text("Decile Groups");


var svg2 = d3.select("#"+chartID).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");
    
    var data = [];
    for (i in dataset) {
             if(dataset[i].group=='PLANNED_UNPLANNED'){
                 data.push(dataset[i]);
           } 
         }
   
      // format the data
      data.forEach(function(d) {
        d.value = +d.value;
      });
    
      // Scale the range of the data in the domains
      x.domain(data.map(function(d) { return d.type; }));
      y.domain([0, d3.max(data, function(d) { return d.value; })]);
    
      // append the rectangles for the bar chart
      svg2.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.type); })
          .attr("width", x.bandwidth())
          .attr("y", function(d) { return y(d.value); })
          .attr("height", function(d) { return height - y(d.value); })
          .attr("fill","#3cb371");

     svg2.selectAll(".text")  		
	  .data(data)
	  .enter()
	  .append("text")
	  .attr("class","label")
	  .attr("x", (function(d) { return x(d.type)-10 + x.bandwidth() / 2 ; }  ))
	  .attr("y", function(d) { return y(d.value) -10; })
	  .attr("dy", ".75em")
	  .text(function(d) { return d.value; });  

  // add the x Axis
  svg2.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))	  
      .selectAll("text")	
        .style("text-anchor", "middle")
		 .attr("class","xlabelbar")
      .select(".domain")
      .remove();


	// Y axis label
	svg2.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 5 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .attr("class","sidelabel")
      .style("text-anchor", "middle")
      .text("Call Type");

var svg3 = d3.select("#"+chartID).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");
    
    var data = [];
    for (i in dataset) {
             if(dataset[i].group=='CALL_TYPE_DESCRIPTION'){
                 data.push(dataset[i]);
           } 
         }
   
      // format the data
      data.forEach(function(d) {
        d.value = +d.value;
      });
    
      // Scale the range of the data in the domains
      x.domain(data.map(function(d) { return d.type; }));
      y.domain([0, d3.max(data, function(d) { return d.value; })]);
    
      // append the rectangles for the bar chart
      svg3.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.type); })
          .attr("width", x.bandwidth())
          .attr("y", function(d) { return y(d.value); })
          .attr("height", function(d) { return height - y(d.value); })
           .attr("fill","#3cb371");

     svg3.selectAll(".text")  		
	  .data(data)
	  .enter()
	  .append("text")
	  .attr("class","label")
	  .attr("x", (function(d) { return x(d.type)-10 + x.bandwidth() / 2 ; }  ))
	  .attr("y", function(d) { return y(d.value) -10; })
	  .attr("dy", ".75em")
	  .text(function(d) { return d.value; });  


  // add the x Axis
  svg3.append("g")
      .attr("class", "axisCSS")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll(".tick text")
      .call(wrap, x.bandwidth())
       .select(".domain")
      .remove();

	// Y axis label
	svg3.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 5 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .attr("class","sidelabel")
      .style("text-anchor", "middle")
      .text("Call Category");
}


function wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}
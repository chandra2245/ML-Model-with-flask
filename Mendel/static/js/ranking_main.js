


queue()
	.defer(d3.json, scatterchartDataUrl)
   .await(ready);

function ready(error, dataset) {
    scatterplotChart('#ScatterPlot',dataset);

}
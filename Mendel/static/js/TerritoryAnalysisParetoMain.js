

queue()
	.defer(d3.json, paretochartDataUrl)
    .await(ready);

function ready(error, datasetParetoChart) {
	d3ParetoChart(datasetParetoChart,'paretoChart');
}
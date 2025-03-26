// Load AOI and AGB images
var aoi = ee.FeatureCollection('projects/ee-komba/assets/bbox_wirong').geometry();
var agb_2021_model = ee.Image('projects/ee-komba/assets/AGB_2021');
var cci_agb = ee.ImageCollection('projects/sat-io/open-datasets/ESA/ESA_CCI_AGB')
  .filterDate('2021-01-01', '2021-12-31')
  .first()
  .select('AGB');

// Visualization palette
var palette = ["#C6ECAE","#A1D490","#7CB970","#57A751","#348E32", "#267A29","#176520","#0C4E15","#07320D","#031807"];

// Map layers
Map.centerObject(aoi, 12);
Map.addLayer(cci_agb.clip(aoi), {min: 0, max: 450, palette: palette}, 'CCI AGB 2021 (Mg/ha)');
Map.addLayer(agb_2021_model.clip(aoi), {min: 0, max: 450, palette: palette}, 'Model AGB 2021 (Mg/ha)');
Map.addLayer(agb_2021_model.subtract(cci_agb).clip(aoi), 
  {min: -100, max: 100, palette: ['red', 'white', 'blue']}, 'Model - CCI Difference');

// Create 500m grid using constant image
var grid = ee.Image.constant(1).clip(aoi).reduceToVectors({
  geometry: aoi,
  scale: 500,
  geometryType: 'polygon',
  eightConnected: false,
  labelProperty: 'grid_id',
  reducer: ee.Reducer.countEvery()
});

// Select and rename bands
var agb_model = agb_2021_model.select('AGB_MgHa').rename('Model_AGB');
var cci_agb_layer = cci_agb.rename('CCI_AGB');

// Combine both into one image
var combined = agb_model.addBands(cci_agb_layer);

// Sample random points within AOI
var samples = combined.sample({
  region: aoi,
  scale: 100,
  numPixels: 1000,
  seed: 42,
  geometries: true
}).filter(ee.Filter.notNull(['Model_AGB', 'CCI_AGB']));

// Scatter plot
var chart = ui.Chart.feature.byFeature(samples, 'Model_AGB', ['CCI_AGB'])
  .setChartType('ScatterChart')
  .setOptions({
    title: 'Model vs CCI AGB (Mg/ha)',
    hAxis: {title: 'Model AGB (Mg/ha)'},
    vAxis: {title: 'CCI AGB (Mg/ha)'},
    pointSize: 3,
    dataOpacity: 0.6,
    trendlines: {0: {showR2: true, visibleInLegend: true}}
  });

print(chart);

// Export sampled points to Drive
Export.table.toDrive({
  collection: samples,
  description: 'AGB_Model_vs_CCI_SamplePoints',
  fileFormat: 'CSV'
});



// Define area of interest
var aoi = ee.FeatureCollection('projects/ee-komba/assets/bbox_wirong').geometry();

// Date range
var start = '2024-01-01';
var end = '2024-03-01';

// Sentinel-2 surface reflectance collection
var s2_raw = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(aoi)
  .filterDate(start, end)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .median()
  .clip(aoi);

// Rescale reflectance values
var s2 = s2_raw.divide(10000);

// Compute NDVI
var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');

// Compute IRECI with numerical stability
var epsilon = ee.Image.constant(0.0001);
var ireci = s2.expression(
  '(B7 - B4) / ((B5 / (B6 + epsilon)) + epsilon)', {
    'B4': s2.select('B4'),
    'B5': s2.select('B5'),
    'B6': s2.select('B6'),
    'B7': s2.select('B7'),
    'epsilon': epsilon
}).rename('IRECI');

// Compute EVI with denominator safety and clamp
var evi = s2.expression(
  '2.5 * ((NIR - RED) / max((NIR + 6 * RED - 7.5 * BLUE + 1), 0.0001))', {
    'NIR': s2.select('B8'),
    'RED': s2.select('B4'),
    'BLUE': s2.select('B2')
}).rename('EVI').clamp(0, 1);

// Compute LAI from EVI
var lai = evi.multiply(3.618).subtract(0.118).rename('LAI');

// Compute FAPAR and FCOVER from NDVI
var fapar = ndvi.multiply(1.24).subtract(0.168).rename('FAPAR');
var fcover = ndvi.multiply(1.26).subtract(0.18).rename('FCOVER');

// Compute unclamped AGB using regression model
var agb_unclamped = s2.select('B4').multiply(20.176)
  .add(fcover.multiply(6.633))
  .subtract(fapar.multiply(6.180))
  .add(lai.multiply(13.452))
  .subtract(ireci.multiply(6.307))
  .subtract(2.282)
  .rename('AGB');

// Clamp negative values to zero
var agb = agb_unclamped.max(0).multiply(25).rename('AGB_MgHa');



// Print AGB value range to console
agb.reduceRegion({
  reducer: ee.Reducer.minMax(),
  geometry: aoi,
  scale: 20,
  bestEffort: true
}).evaluate(function(stats) {
  print('Final Above-Ground Biomass (ton/pixel) - Value Range:', stats);
});

// Visualization
Map.centerObject(aoi, 12);
Map.addLayer(agb, {min: 0, max: 80, palette: ['white', 'green']}, 'Above-Ground Biomass');

Export.image.toAsset({
  image: agb,
  description: 'AGB_2021_export',
  assetId: 'projects/ee-komba/assets/AGB_2021',
  region: aoi,
  scale: 100,  // match CCI resolution (1 ha = 100 m)
  maxPixels: 1e13
});


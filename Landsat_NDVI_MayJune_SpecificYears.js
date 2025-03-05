// Script showing how to obtain a harmonized Landsat Time-Series
// using Landsat Collection 2 with NDVI for specific years.

// Area of Interest (AOI)
var geometry = ee.FeatureCollection('projects/ee-komba/assets/bbox_wirong').geometry();

// Asset path to save images
var assetPath = 'projects/ee-komba/assets/kaya/';

// Years for which to create NDVI images
var years = [2013, 2015, 2017, 2019, 2021, 2023];

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 1: Select the Landsat dataset
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// Landsat Collection 2 Tier-1 Scenes
var L5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2');
var L7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2');
var L8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 2: Data Pre-Processing and Cloud Masking
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// Mapping of band-names to a uniform naming scheme
var l5Bands = ['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B7'];
var l5names = ['blue','green','red','nir','swir1','swir2'];

var l7Bands = ['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B7'];
var l7names = ['blue','green','red','nir','swir1','swir2'];

var l8Bands = ['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7'];
var l8names = ['blue','green','red','nir','swir1','swir2'];

// Cloud masking function for Landsat 4,5 and 7
function maskL457sr(image) {
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);

  // Apply the scaling factors to the appropriate bands.
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);

  // Replace the original bands with the scaled ones and apply the masks.
  return image.addBands(opticalBands, null, true)
      .addBands(thermalBand, null, true)
      .updateMask(qaMask)
      .updateMask(saturationMask)
      .copyProperties(image, ['system:time_start']);
}

// Cloud masking function for Landsat 8
function maskL8sr(image) {
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);

  // Apply the scaling factors to the appropriate bands.
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);

  // Replace the original bands with the scaled ones and apply the masks.
  return image.addBands(opticalBands, null, true)
      .addBands(thermalBands, null, true)
      .updateMask(qaMask)
      .updateMask(saturationMask)
      .copyProperties(image, ['system:time_start']);
}

// Apply filters, cloud-mask and rename bands
var L5 = L5
  .filter(ee.Filter.lt('WRS_ROW', 122))  // Remove night-time images.
  .map(maskL457sr)
  .select(l5Bands,l5names);

var L7 = L7
  .filter(ee.Filter.lt('WRS_ROW', 122))  // Remove night-time images.
  .filter(ee.Filter.date('1984-01-01', '2017-01-01'))  // Orbital drift after 2017.
  .map(maskL457sr)
  .select(l7Bands,l7names);

var L8 = L8
  .filter(ee.Filter.date('2013-05-01', '2099-01-01')) // Images before May 1 had some pointing issues.
  .filter(ee.Filter.neq('NADIR_OFFNADIR', 'OFFNADIR'))
  .filter(ee.Filter.lt('WRS_ROW', 122))  // Remove night-time images.
  .map(maskL8sr)
  .select(l8Bands,l8names);

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 3: Select Date Ranges, Filter and Merge
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var merged = L5.merge(L7).merge(L8).filter(ee.Filter.bounds(geometry));

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 4: Create NDVI Images for Specific Years (May-June) and Export
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

years.forEach(function(year) {
  var startDate = ee.Date.fromYMD(year, 5, 1);
  var endDate = ee.Date.fromYMD(year, 7, 1); // June 30th
  var yearFiltered = merged.filter(ee.Filter.date(startDate, endDate));
  var composite = yearFiltered.median().clip(geometry);

  // Calculate NDVI
  var ndvi = composite.normalizedDifference(['nir', 'red']).rename('NDVI');

  // Create an image with only the NDVI band
  var ndviImage = ndvi.set({
    'year': year,
    'system:time_start': startDate.millis(),
    'system:time_end': endDate.millis()
  });

  // Export the NDVI image as an asset
  Export.image.toAsset({
    image: ndviImage,
    description: 'NDVI_' + year,
    assetId: assetPath + 'NDVI_' + year,
    region: geometry,
    scale: 30,
    maxPixels: 1e13
  });
});

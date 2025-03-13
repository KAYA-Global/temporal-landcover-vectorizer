// Script to obtain NDVI composites from Landsat 8 and 9 (January–April) at 100m resolution

// Define Area of Interest (AOI)
var geometry = ee.FeatureCollection('projects/ee-komba/assets/bbox_wirong').geometry();

// Define asset path for saving images
var assetPath = 'projects/ee-komba/assets/kaya/';

// Define years for which to create NDVI images
var years = [2013, 2015, 2017, 2019, 2021, 2023];

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 1: Select Landsat 8 & 9 Data
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// Landsat Collection 2 Tier-1 Surface Reflectance
var L8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');
var L9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');

// Define band names for harmonization
var l89Bands = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'];
var l89names = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'];

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 2: Cloud Masking Function
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function maskL89sr(image) {
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);

  // Apply the scaling factors
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);

  // Return the masked and scaled image
  return image.addBands(opticalBands, null, true)
      .addBands(thermalBands, null, true)
      .updateMask(qaMask)
      .updateMask(saturationMask)
      .copyProperties(image, ['system:time_start']);
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 3: Apply Filters and Process Landsat 8 & 9
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var L8 = L8
  .filter(ee.Filter.date('2013-01-01', '2099-01-01')) // Landsat 8 available since 2013
  .filter(ee.Filter.neq('NADIR_OFFNADIR', 'OFFNADIR'))
  .filter(ee.Filter.lt('WRS_ROW', 122))  // Remove night-time images
  .map(maskL89sr)
  .select(l89Bands, l89names);

var L9 = L9
  .filter(ee.Filter.date('2021-01-01', '2099-01-01')) // Landsat 9 operational since 2021
  .filter(ee.Filter.neq('NADIR_OFFNADIR', 'OFFNADIR'))
  .filter(ee.Filter.lt('WRS_ROW', 122))  // Remove night-time images
  .map(maskL89sr)
  .select(l89Bands, l89names);

// Merge collections
var merged = L8.merge(L9).filter(ee.Filter.bounds(geometry));

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Step 4: Create NDVI Composites for January–April and Export
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

years.forEach(function(year) {
  var startDate = ee.Date.fromYMD(year, 1, 1);
  var endDate = ee.Date.fromYMD(year, 5, 31);
  
  var yearFiltered = merged.filter(ee.Filter.date(startDate, endDate));
  var composite = yearFiltered.median().clip(geometry); // Median composite for Jan–Apr

  // Calculate NDVI
  var ndvi = composite.normalizedDifference(['nir', 'red']).rename('NDVI');

  // Create an image with only the NDVI band
  var ndviImage = ndvi.set({
    'year': year,
    'system:time_start': startDate.millis(),
    'system:time_end': endDate.millis()
  });

  // Export the NDVI image as an asset at 100m resolution
  Export.image.toAsset({
    image: ndviImage,
    description: 'NDVI_JanApr_' + year,
    assetId: assetPath + 'NDVI_JanApr_' + year,
    region: geometry,
    scale: 100,  // Export at 100m resolution
    maxPixels: 1e13
  });
});

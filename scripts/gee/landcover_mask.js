// Load the feature collection containing the polygons
var polygons = ee.FeatureCollection('projects/ee-komba/assets/kaya/wirong/mask_5_8');

// Load the WorldCover data and get the first image
var worldcover = ee.ImageCollection("ESA/WorldCover/v200").first();

// Create a mask for the desired land cover classes (10: Tree Cover, 20: Shrubland, 30: Grassland, 60: Bare/Sparse Vegetation)
var landCoverMask = worldcover.eq(10).or(worldcover.eq(20)).or(worldcover.eq(30)).or(worldcover.eq(60));

// List of Landsat images to process
var images = {
  2013: ee.Image('projects/ee-komba/assets/kaya/NDVI_2013'),
  2015: ee.Image('projects/ee-komba/assets/kaya/NDVI_2015'),
  2017: ee.Image('projects/ee-komba/assets/kaya/NDVI_2017'),
  2019: ee.Image('projects/ee-komba/assets/kaya/NDVI_2019'),
  2021: ee.Image('projects/ee-komba/assets/kaya/NDVI_2021'),
  2023: ee.Image('projects/ee-komba/assets/kaya/NDVI_2023')
};

// Add visualization layers
Map.addLayer(polygons, {color: 'blue'}, 'Original Polygons');
Map.addLayer(landCoverMask.selfMask(), {palette: ['green']}, 'Land Cover Mask');

// Center map on the area of interest
Map.centerObject(polygons);

// Process each polygon
polygons.evaluate(function(features) {
  features.features.forEach(function(feature) {
    var areaNum = feature.properties.Area;
    var geom = ee.Geometry(feature.geometry);
    
    // Process each year
    Object.keys(images).forEach(function(year) {
      var image = images[year];
      
      // Apply both the land cover mask and clip to the polygon
      var masked = image
        .updateMask(landCoverMask)
        .clip(geom);
      
      // Export the masked image
      Export.image.toDrive({
        image: masked,
        description: 'NDFI_Masked_' + year + '_' + areaNum,
        scale: 100,
        region: geom,
        folder: 'earthengine',
        maxPixels: 1e13
      });
    });
  });
});

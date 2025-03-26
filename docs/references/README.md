# References

This directory contains research papers and other reference materials that inform the methodology used in this project.

## Publications

### Above-Ground Biomass Estimation

1. **2022_Rojas_EstimationAGBTropicalDryForests.pdf**  
   *Estimation of aboveground biomass in tropical dry forests using Sentinel-2 and biophysical variables derived from remote sensing data*  
   Authors: M. R., J. M., et al.  
   Journal: Environmental Monitoring and Assessment (2022)  
   DOI: [10.1007/s40068-022-00250-y](https://doi.org/10.1007/s40068-022-00250-y)  
   
   This paper provides the methodology for estimating above-ground biomass (AGB) using Sentinel-2 surface reflectance and derived vegetation indices. The model is implemented in `scripts/gee/3. AGB_Model_Sentinel2_Template.js` and validated against ESA CCI data in `scripts/gee/4. AGB_Model_Comparison_vCCI.js`. 
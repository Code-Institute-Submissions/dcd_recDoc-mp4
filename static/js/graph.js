//==========DEFER DATA using queue FUNCTION=================
queue()
        .defer(d3.json, "/recipe_book/recipes")
        .await(deriveGraphs);
//SET UP THE MAKE GRAPH FUNCTION and insert data once loaded
//change stringdata type to datetime object (not used yet but may be in the future)
var dateFormat = d3.time.format("%d-%m-Y");
function deriveGraphs(error, recipesJson) {
    //create crossfilter instance
    var ndx = crossfilter(recipesJson);
     recipesJson.forEach(function (d) {
                 d["Date_added"] = dateFormat.parse(d["Date_added"]);
    });
    //call functions to render graphs
    total_all_recipes(ndx);
    total_vege_recipes(ndx);
    total_vegan_recipes(ndx);
    show_pie_cat(ndx);
    show_allergens(ndx);
    show_country_of_origin(ndx);
    type_by_category(ndx);
    type_by_allergen(ndx);
dc.renderAll();
}
//DERIVE FUNCTIONS TO RENDER GRAPHS
//calculate and display total number of recipes
function total_all_recipes(ndx) { 
    var all = ndx.groupAll();
    dc.numberDisplay("#all-recipes")
      .formatNumber(d3.format("d"))
      .valueAccessor(function(d){return d; })
      .group(all);
}
//calculate and display total number of Vegetarian recipes
function total_vege_recipes(ndx) {
    var veg = ndx.groupAll(dc.pluck('Suitable_for_Vegetarians'));
    dc.numberDisplay("#veg-recipes")
      .formatNumber(d3.format("d"))
      .valueAccessor(function(d){return d; })
      .group(ndx.groupAll().reduceSum(function(d) {
          count = 0
          if (d.Suitable_for_Vegetarians ==="Yes") {
              count++
              return count
          } else {
              return 0;
          }
      }));
}
//calculate and display total number of Vegan recipes
function total_vegan_recipes(ndx) {
     var vegan = ndx.groupAll(dc.pluck('Suitable_for_Vegans'));
    dc.numberDisplay("#vegan-recipes")
      .formatNumber(d3.format("d"))
      .valueAccessor(function(d){return d; })
      .group(ndx.groupAll().reduceSum(function(d) {
          count = 0
          if (d.Suitable_for_Vegans ==="Yes") {
              count++
              return count
          } else {
              return 0;
          }
      }));
}
//simple pie chart showing number of recipes per category
function show_pie_cat(ndx) {
    var dim = ndx.dimension(dc.pluck('category_name'));
    var group = dim.group();
 dc.pieChart("#pie-cat")
            .height(300)
            .radius(120)
            .innerRadius(50)
            .transitionDuration(1500)
            .dimension(dim)
            .group(group)
            .label(function(d){return d.value})
            .legend(dc.legend().x(100).y(0).itemHeight(13).gap(5));

    
}
//simple pie chart showing number and type of allergen 
function show_allergens(ndx) {
    var dim = ndx.dimension(dc.pluck('Allergens'));
    var group = dim.group();
    dc.pieChart("#allergens")
        .height(300)
        .radius(120)
        .innerRadius(50)
        .transitionDuration(1500)
        .dimension(dim)
        .group(group)
        .label(function(d){return d.value})
        .legend(dc.legend().x(10).y(0).itemHeight(13).gap(5).autoItemWidth(false));
}             
//bar chart showing number of recipes by country of origin
function show_country_of_origin(ndx) {
    var dim = ndx.dimension(dc.pluck('Country_of_origin'));
    var group = dim.group();
    dc.barChart("#origin")
        .width(600)
        .height(250)
        .margins({top: 10, right: 50, bottom: 40, left: 50})
        .dimension(dim)
        .group(group)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .ordinalColors(['#26a69a'])
        .xAxisLabel("Recipe Country of origin")
        .yAxisLabel("No of recipes")
        .yAxis().ticks(10);
}
//bar chart showing type by category
function type_by_category(ndx) {
    var cat_dim = ndx.dimension(dc.pluck('category_name'));
            function totVeg(Suitable_for_Vegetarians) {
                return function (d) {
                    countV = 0
                   if (d.Suitable_for_Vegetarians === "Yes") {
                     countV++;
                     return countV
                 } else {
                     return 0;
                 } 
                };
            }
        var    totVegetarian = cat_dim.group().reduceSum(totVeg('Yes'));
            function totVegan(Suitable_for_Vegans) {
                return function (d) {
                    countv = 0
                   if (d.Suitable_for_Vegans === "Yes") {
                     countv++;
                     return countv
                 } else {
                     return 0;
                 } 
                };
            }
        var    totalVegan = cat_dim.group().reduceSum(totVegan('Yes'));
             function totMeat(Suitable_for_Vegetarians) {
                return function (d) {
                    countT = 0
                   if (d.Suitable_for_Vegetarians === "No") {
                     countT++;
                     return countT
                 } else {
                     return 0;
                 } 
                };
            }
        var    totalMeat = cat_dim.group().reduceSum(totMeat('No'));
            
    //var group = dim.group();
    dc.barChart("#type")
        .width(450)
        .height(400)
        .margins({top: 10, right: 50, bottom: 40, left: 50})
        .dimension(cat_dim)
        .group(totalMeat, 'Other')
        .stack(totVegetarian, 'Vegetarian')
        .stack(totalVegan, 'Vegan')
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .title(function(d) { return d.key +" number of recipes is "+ d.value; })
         .legend(dc.legend().x(70).y(0).itemHeight(10).gap(3))
        .xAxisLabel("Recipe Category")
        .yAxisLabel("No of recipes")
        .yAxis().ticks(10);
}
function type_by_allergen(ndx) {
    var allergen_dim = ndx.dimension(dc.pluck('Allergens'));
            function totVeg(Suitable_for_Vegetarians) {
                return function (d) {
                    countV = 0
                   if (d.Suitable_for_Vegetarians === "Yes") {
                     countV++;
                     return countV
                 } else {
                     return 0;
                 } 
                };
            }
            function totVegan(Suitable_for_Vegans) {
                return function (d) {
                    countv = 0
                   if (d.Suitable_for_Vegans === "Yes") {
                     countv++;
                     return countv
                 } else {
                     return 0;
                 } 
                };
            }
             function totMeat(Suitable_for_Vegetarians) {
                return function (d) {
                    countT = 0
                   if (d.Suitable_for_Vegetarians === "No") {
                     countT++;
                     return countT
                 } else {
                     return 0;
                 } 
                };
            }
    var  totVegetarian = allergen_dim.group().reduceSum(totVeg('Yes'));
    var totalVegan = allergen_dim.group().reduceSum(totVegan('Yes'));
    var totalMeat = allergen_dim.group().reduceSum(totMeat('No'));
     
    
 //var group = dim.group();
    dc.barChart("#typebyAllergen")
        .width(450)
        .height(400)
        .margins({top: 10, right: 50, bottom: 100, left: 50})
        .dimension(allergen_dim)
         .group(totalMeat, 'Other')
        .stack(totVegetarian, 'Vegetarian')
        .stack(totalVegan, 'Vegan')
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .title(function(d) { return d.key +" number of recipes is "+ d.value; })
         .legend(dc.legend().x(70).y(0).itemHeight(10).gap(3))
        .yAxisLabel("No of recipes")
        .yAxis().ticks(10);
}

    
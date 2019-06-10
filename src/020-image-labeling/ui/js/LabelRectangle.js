/**
 * @class example.connection_labeledit.LabelConnection
 * 
 * A simple Connection with a label wehich sticks in the middle of the connection..
 *
 * @author Andreas Herz
 * @extend draw2d.Connection
 */
var LabelRectangle = draw2d.shape.basic.Rectangle.extend({
    
    init:function(attr)
    {
      this._super($.extend({
          bgColor:null,
          stroke:3,
          color:"#1ca1c1"
      },attr));
    
      // Create any Draw2D figure as decoration for the connection
      //
      this.label = new draw2d.shape.basic.Label({
          text:"I'm a Label",
          bgColor:"#1ca1c1",
          stroke:0,
          fontColor:"#ffffff"});
      
      // add the new decoration to the connection with a position locator.
      //
      this.add(this.label, new draw2d.layout.locator.XYAbsPortLocator(-1,-20));
      
      this.label.installEditor(new draw2d.ui.LabelInplaceEditor());
    }
});

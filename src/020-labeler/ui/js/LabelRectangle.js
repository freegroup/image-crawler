/**
 * @class example.connection_labeledit.LabelConnection
 * 
 * A simple Connection with a label wehich sticks in the middle of the connection..
 *
 * @author Andreas Herz
 * @extend draw2d.Connection
 */
var LabelRectangle = draw2d.shape.basic.Rectangle.extend({
    NAME: "LabelRectangle",

    init:function(attr)
    {
      this._super($.extend({
          stroke:3,
          bgColor:"rgba(28,161,193,0.3)",
          color:"#1ca1c1"
      },attr));

      // Create any Draw2D figure as decoration for the connection
      //
      this.label = new draw2d.shape.basic.Label({
          text: attr?attr.text:"undefined",
          bgColor:"#1ca1c1",
          stroke:0,
          fontColor:"#ffffff"});
      
      // add the new decoration to the connection with a position locator.
      //
      this.add(this.label, new draw2d.layout.locator.XYAbsPortLocator(-1,-20));
      
      this.label.installEditor(new draw2d.ui.LabelInplaceEditor());
    },

    getPersistentAttributes : function()
    {
        var memento = this._super();

        // add all decorations to the memento
        //
        memento.text = this.label.getText()

        return memento;
    },
    /**
     * @method
     * Read all attributes from the serialized properties and transfer them into the shape.
     *
     * @param {Object} memento
     * @returns
     */
    setPersistentAttributes : function(memento)
    {
        this._super(memento);

        this.label.setText(memento.text);
    }
});

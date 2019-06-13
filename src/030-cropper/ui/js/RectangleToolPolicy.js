
var RectangleToolPolicy = draw2d.policy.canvas.BoundingboxSelectionPolicy.extend({

  init: function () {
    this._super()

    this.topLeftPoint = null
    this.boundingBoxFigure1 = null
    this.boundingBoxFigure2 = null
  },



  /**
   * @method
   *
   * @param {draw2d.Canvas} canvas
   * @param {Number} x the x-coordinate of the mouse down event
   * @param {Number} y the y-coordinate of the mouse down event
   * @param {Boolean} shiftKey true if the shift key has been pressed during this event
   * @param {Boolean} ctrlKey true if the ctrl key has been pressed during the event
   */
  onMouseDown: function (canvas, x, y, shiftKey, ctrlKey) {
    this.topLeftPoint = new draw2d.geo.Point(x, y)
    this._super(canvas, x, y, shiftKey, ctrlKey)
  },

  /**
   * @method
   *
   * @param {draw2d.Canvas} canvas
   * @param {Number} x the x-coordinate of the mouse down event
   * @param {Number} y the y-coordinate of the mouse down event
   * @template
   */
  onMouseUp: function (canvas, x, y, shiftKey, ctrlKey) {
    if (this.boundingBoxFigure1 !== null) {
      this.boundingBoxFigure1.setCanvas(null);
      this.boundingBoxFigure1 = null;
      this.boundingBoxFigure2.setCanvas(null);
      this.boundingBoxFigure2 = null;
    }

    if (shiftKey === true && this.mouseDownElement === null) {
      var bottomRight = new draw2d.geo.Point(x, y)
      if (this.topLeftPoint.distance(bottomRight) > 3) {
        var rect = new LabelRectangle({
            text: document.getElementById(currentLabelInput).value,
            x: this.topLeftPoint.x,
            y: this.topLeftPoint.y,
            width: bottomRight.x - this.topLeftPoint.x,
            height: bottomRight.y - this.topLeftPoint.y
        })
        var command = new draw2d.command.CommandAdd(canvas, rect, rect.getX(), rect.getY())
        canvas.getCommandStack().execute(command)
        canvas.setCurrentSelection(rect)
      }
    }
    else{
        this._super(canvas, x, y, shiftKey, ctrlKey)
    }

    this.topLeftPoint = null
  }
})





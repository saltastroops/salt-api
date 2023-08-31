import { Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: "wm-finder-chart-view",
  templateUrl: "./finder-chart-view.component.html",
  styleUrls: ["./finder-chart-view.component.scss"],
})
export class FinderChartViewComponent implements OnInit {
  @ViewChild("image", { static: false }) finderChartImage!: ElementRef;
  finderChartUrl!: string;
  positionAngle = 0;
  rotationValue = 0;
  zoomScale = 1;
  mirrorX = 1;
  mirrorY = 1;
  message = "";
  readonly maxScale = 3;
  readonly minScale = 0.5;
  readonly scaleDelta = 0.1;
  isDragging = false;
  startX = 0;
  startY = 0;
  translateX = 0;
  translateY = 0;
  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.positionAngle = params.positionAngle || 0;
      this.rotationValue = params.positionAngle || 0;
      this.finderChartUrl = params.finderChart;
    });
  }

  setFinderChartTransform(transformation: {
    transform: string;
    value: number;
  }): void {
    if (transformation.transform === "zoom") {
      if (this.zoomScale < this.maxScale && transformation.value > 0) {
        this.zoomScale += this.scaleDelta;
      } else if (this.zoomScale > this.minScale && transformation.value < 0) {
        this.zoomScale -= this.scaleDelta;
      }
    }
    if (transformation.transform === "rotate") {
      this.rotationValue = transformation.value;
    }
    if (transformation.transform === "mirrorX") {
      this.mirrorX = this.mirrorX === -1 ? 1 : -1;
    }
    if (transformation.transform === "mirrorY") {
      this.mirrorY = this.mirrorY === -1 ? 1 : -1;
    }
  }

  onWheelZoom(event: WheelEvent): void {
    event.preventDefault();
    this.setFinderChartTransform({ transform: "zoom", value: event.deltaY });
  }

  onMouseDown(event: MouseEvent): void {
    event.preventDefault();
    this.isDragging = true;
    this.startX = event.clientX - this.translateX;
    this.startY = event.clientY - this.translateY;
    this.updateCursor("grabbing");
  }

  onMouseUp(): void {
    this.isDragging = false;
    this.updateCursor("grab");
  }

  onMouseMove(event: MouseEvent): void {
    if (this.isDragging) {
      this.translateX = event.clientX - this.startX;
      this.translateY = event.clientY - this.startY;
    }
  }

  getTransform(): string {
    return `scale(${this.zoomScale}) translate(${this.translateX}px, ${this.translateY}px) rotate(${this.rotationValue}deg) scaleX(${this.mirrorX}) scaleY(${this.mirrorY})`;
  }

  private updateCursor(cursorStyle: string) {
    document.body.style.cursor = cursorStyle;
  }

  protected readonly parseFloat = parseFloat;
}

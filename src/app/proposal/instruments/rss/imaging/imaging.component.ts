import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-imaging",
  templateUrl: "./imaging.component.html",
  styleUrls: ["./imaging.component.scss"],
})
export class ImagingComponent {
  @Input() filter!: string;
}

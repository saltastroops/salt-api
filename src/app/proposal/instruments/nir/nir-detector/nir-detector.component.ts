import { Component, Input } from '@angular/core';
import {NirDetector} from "../../../../types/nir";

@Component({
  selector: 'wm-nir-detector',
  templateUrl: './nir-detector.component.html',
  styleUrls: ['./nir-detector.component.scss']
})
export class NirDetectorComponent {

  @Input() nirDetector!: NirDetector;
}

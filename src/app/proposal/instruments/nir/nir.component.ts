import {Component, Input} from '@angular/core';
import {PayloadConfiguration} from "../../../types/observation";
import {Nir} from "../../../types/nir";

@Component({
  selector: 'wm-nir',
  templateUrl: './nir.component.html',
  styleUrls: ['./nir.component.scss']
})
export class NirComponent {
  @Input() nir!: Nir;
  @Input() payloadConfiguration!: PayloadConfiguration;
}

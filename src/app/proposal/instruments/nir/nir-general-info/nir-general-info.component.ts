import {Component, Input} from '@angular/core';
import {Nir, NirProcedure} from "../../../../types/nir";

@Component({
  selector: 'wm-nir-general-info',
  templateUrl: './nir-general-info.component.html',
  styleUrls: ['./nir-general-info.component.scss']
})
export class NirGeneralInfoComponent {

  @Input() nir!: Nir;

}

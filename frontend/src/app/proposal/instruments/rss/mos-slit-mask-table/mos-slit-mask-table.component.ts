import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-mos-slit-mask-table',
  templateUrl: './mos-slit-mask-table.component.html',
  styleUrls: ['./mos-slit-mask-table.component.scss']
})
export class MosSlitMaskTableComponent implements OnInit {
  @Input() mosSlitMask: {
    type: string;
    barcode: string
    mask: {
      image: string;
      xml: string;
      cutBy: string | null;
      cutDate: Date;
      comment: string | null;
      edgeLength: string;
    }
  } = {
    type: 'Mos', barcode: 'P001234N001',
    mask: {
      image: 'image uri',
      xml: 'xml uri',
      cutBy: 'John Doe',
      cutDate: new Date(2020, 7, 11, 12, 30, 55),
      comment: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.',
      edgeLength: '5'
    }
  };
  constructor() { }

  ngOnInit(): void {
  }

}

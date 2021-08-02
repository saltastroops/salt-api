import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-payload-configuration-table',
  templateUrl: './payload-configuration-table.component.html',
  styleUrls: ['./payload-configuration-table.component.scss']
})
export class PayloadConfigurationTableComponent implements OnInit {
  @Input() payload: Payload = {
    minimumUsefulTime: 300,
    positionAngles: [10],
    constraints: undefined,
    dataAccessMethod: 'Normal',  // TODO this need to be an enum.
    docFormat: 'HTML',  // TODO this need to be an enum.
    shutterOpenTime: 2000,
    overhead: 2000,
    charged: 2000,
    chats: [
      {
        path: '/assets/noun_Night_771441.png',
        comment: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium beatae cupiditate dolorum earum ' +
          'itaque, maxime nulla officiis vitae voluptate voluptatibus?\n',
        validFrom: new Date(2021, 8, 8, 12, 0),
        validUntil: new Date(2021, 8, 20, 22, 0),
      },
      {
        path: '/assets/noun_Night_771441.png',
        comment: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium beatae cupiditate dolorum earum ' +
          'itaque, maxime nulla officiis vitae voluptate voluptatibus?\n',
        validFrom: new Date(2021, 8, 8, 12, 0),
        validUntil: new Date(2021, 8, 20, 22, 0),
      },
    ]
  };
  firstValidFrom: Date | undefined;
  lastValidUntil: Date | undefined;
  constructor() { }

  ngOnInit(): void {
    this.firstValidFrom = this.payload.chats.reduce((prev, curr) => {
      return prev.validFrom < curr.validFrom ? prev : curr;
    }).validFrom;
    this.lastValidUntil = this.payload.chats.reduce((prev, curr) => {
      return prev.validUntil < curr.validUntil ? prev : curr;
    }).validUntil;

    console.log(this.payload.chats);

  }

}

interface Payload {
  minimumUsefulTime: number;
  positionAngles: number[];
  constraints: string | undefined;
  dataAccessMethod: string;  // TODO this need to be an enum.
  docFormat: string;  // TODO this need to be an enum.
  shutterOpenTime: number;
  overhead: number;
  charged: number;
  chats: {
    path: string;
    comment: string;
    validFrom: Date;
    validUntil: Date;
  }[];

}

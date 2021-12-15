import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'nl2br',
})
export class nl2brPipe implements PipeTransform {
  transform(value: string): string {
    if (value) {
      return value.trim().replace(/\n/g, '<br/>');
    } else {
      return '';
    }
  }
}

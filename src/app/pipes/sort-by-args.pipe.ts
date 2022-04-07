import { Pipe, PipeTransform } from "@angular/core";

import { byPropertiesOf } from "../utils";

@Pipe({
  name: "sortByArgs",
})
export class SortByArgsPipe implements PipeTransform {
  transform<T>(array: Array<T>, ...args: string[]): T[] {
    const sortedArray = array ? [...array] : [];
    sortedArray?.sort((a, b) => byPropertiesOf(args)(a as never, b as never));
    return sortedArray;
  }
}

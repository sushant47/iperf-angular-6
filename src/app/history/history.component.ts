import { Component, OnInit, Input } from '@angular/core';
import { RestService } from '../shared/services/rest.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  @Input() historylist: any;

  constructor(private restService: RestService) { }

  ngOnInit() {
  }

  public gettingHistory() {
    this.restService.get('http://127.0.0.1:5000/historygetter').subscribe((data: any) => {
      this.historylist = data.historylist;
    });
  }
}

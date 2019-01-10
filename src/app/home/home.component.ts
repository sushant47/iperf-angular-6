import { Component, OnInit } from '@angular/core';
import { RestService } from '../shared/services/rest.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  public serverIP: any;
  public serverPORT: any;
  public output: any = {};
  public historylist: any;
  public loading: Boolean = false;
  constructor(private restService: RestService) { }

  ngOnInit() {
  }

  public sendingIPs() {
    this.loading = true;
    const val = {
      serverIP: this.serverIP,
      serverPORT: this.serverPORT
    };
    this.restService.post('http://127.0.0.1:5000/ipsender', val)
      .subscribe((data: any) => {
        console.log(data);
        this.output = data;
        this.getHistory();
      });
  }
  public getHistory() {
    this.restService.get('http://127.0.0.1:5000/historygetter').subscribe((data: any) => {
      this.loading = false;
      this.historylist = data.historylist;
    });
  }
}

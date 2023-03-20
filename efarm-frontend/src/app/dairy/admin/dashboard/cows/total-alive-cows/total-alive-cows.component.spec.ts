import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalAliveCowsComponent } from './total-alive-cows.component';

describe('TotalAliveCowsComponent', () => {
  let component: TotalAliveCowsComponent;
  let fixture: ComponentFixture<TotalAliveCowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalAliveCowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TotalAliveCowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyMilkDetailComponent } from './dairy-milk-detail.component';

describe('DairyMilkDetailComponent', () => {
  let component: DairyMilkDetailComponent;
  let fixture: ComponentFixture<DairyMilkDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyMilkDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyMilkDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

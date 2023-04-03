import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyMilkListComponent } from './dairy-milk-list.component';

describe('DairyMilkListComponent', () => {
  let component: DairyMilkListComponent;
  let fixture: ComponentFixture<DairyMilkListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyMilkListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyMilkListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

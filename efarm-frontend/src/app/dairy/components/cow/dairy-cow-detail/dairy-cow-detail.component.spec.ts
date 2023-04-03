import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyCowDetailComponent } from './dairy-cow-detail.component';

describe('DairyCowDeleteComponent', () => {
  let component: DairyCowDetailComponent;
  let fixture: ComponentFixture<DairyCowDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyCowDetailComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyCowDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
